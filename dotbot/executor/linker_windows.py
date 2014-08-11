import os
import win32file # FIXME try catch?
from . import Executor

class LinkerWindows7(Executor):
    '''
    Symbolically links dotfiles.

    Windows functionality differs across releases -- this was meant for
    Windows 7 only.
    '''

    _directive = 'link_windows'

    _attributeSymlinkDir = 1040
    _attributeSymlinkFile = 1056

    def can_handle(self, directive):
        return directive == self._directive and os.name == 'nt'

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Linker cannot handle directive %s' % directive)
        return self._process_links(data)

    def _process_links(self, links):
        success = True
        for destination, source in links.items():
            success &= self._link(source, destination)
        if success:
            self._log.info('All links have been set up')
        else:
            self._log.error('Some links were not successfully set up')
        return success

    def _is_link(self, path):
        '''
        Returns true if the path is a symbolic link.
        '''
        return win32file.GetFileAttributes(os.path.expanduser(path)) in [_attributeSymlinkFile, _attributeSymlinkDir]

    def _link_destination(self, path):
        ############################ FIXME put new logic here

        '''
        Returns the absolute path to the destination of the symbolic link.
        '''
        path = os.path.expanduser(path)
        rel_dest = os.readlink(path)
        return os.path.join(os.path.dirname(path), rel_dest)

    def _exists(self, path):
        ############################ FIXME put new logic here
        # should return false for broken symbolic links

        '''
        Returns true if the path exists.
        '''
        path = os.path.expanduser(path)
        return os.path.exists(path)

    def _link(self, source, link_name):
        '''
        Links link_name to source.

        Returns true if successfully linked files.
        '''
        print 'link source = {}, link name = {}'.format(source, link_name)
        success = False
        source = os.path.join(self._base_directory, source)
        print '--- asdf ---'
        # if symlink of that name already exists, but it's target is not what we want to link it to.
        if (not self._exists(link_name) and self._is_link(link_name) and
                self._link_destination(link_name) != source):
            print '111'
            self._log.warning('Invalid link %s -> %s' %
                (link_name, self._link_destination(link_name)))
        # if symlink doesn't exist and our source does, link it -- making the target the source
        elif not self._exists(link_name) and self._exists(source):
            print '222'
            try:
                ############################ FIXME put new logic here
                os.symlink(source, os.path.expanduser(link_name))
            except AttributeError:
                print 'only supported on linux'
            except OSError as e:
                print type(e)
                self._log.warning('Linking failed %s -> %s' % (link_name, source))
                print '2.111'
            else:
                self._log.lowinfo('Creating link %s -> %s' % (link_name, source))
                success = True
        elif self._exists(link_name) and not self._is_link(link_name):
            print '333'
            self._log.warning(
                '%s already exists but is a regular file or directory' %
                link_name)
        elif self._is_link(link_name) and self._link_destination(link_name) != source:
            print '444'
            self._log.warning('Incorrect link %s -> %s' %
                (link_name, self._link_destination(link_name)))
        elif not self._exists(source):
            print '555'
            if self._is_link(link_name):
                self._log.warning('Nonexistant target %s -> %s' %
                    (link_name, source))
            else:
                self._log.warning('Nonexistant target for %s : %s' %
                    (link_name, source))
        else:
            print '666'
            self._log.lowinfo('Link exists %s -> %s' % (link_name, source))
            success = True
        print '==done link==='
        return success
